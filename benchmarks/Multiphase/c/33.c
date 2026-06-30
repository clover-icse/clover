int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;

    // loop body
    while(unknown()){
        x = x + 1;
        if(z / 100 == x / 100){
            z = z;
        }else{
            z = z + 100;
        }
        y = (y + 1) % 100;
        
    }

    // post-condition
    assert(x == (z + y));
    
}
