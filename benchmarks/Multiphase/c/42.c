int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    z = 0;
    assume(y == z);
    

    // loop body
    while(unknown()){
        if(y >= 5765){
            z = z + 3;
        }else{
            z = z + 2;
        }
        if(x >= 1765){
            y = y + 2;
        }else{
            y = y + 1;
        }
        x = x + 1;   
    }

    // post-condition
    if(x > 17650){
        assert(z > 27650);
    }
    
}