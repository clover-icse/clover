int main(){
    int x, z;

    // pre-conditions
    x = 0;
    z = 0;
    

    // loop body
    while(unknown()){
        if(x * 5 < z){
            x = x + 1;
        }else{
            x = x / 10;
            z = 1 + z;
        }      
    }

    // post-condition
    if(z > 50){
        assert(z > x);
    }
    
}